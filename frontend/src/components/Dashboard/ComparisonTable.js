import React from 'react';

const ComparisonTable = ({ data }) => {
    return (
        <div className="comparison-table">
            <h2>Comparison Table</h2>
            <table>
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Value 1</th>
                        <th>Value 2</th>
                        <th>Difference</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item, index) => (
                        <tr key={index}>
                            <td>{item.name}</td>
                            <td>{item.value1}</td>
                            <td>{item.value2}</td>
                            <td>{item.value1 - item.value2}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default ComparisonTable;